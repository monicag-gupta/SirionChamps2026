package com.example.userinfo;

import jakarta.servlet.http.HttpServletRequest;
import org.springframework.context.MessageSource;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestClient;

import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

@RestController
public class UserInfoController {

    private final RestClient restClient = RestClient.create();
    private final MessageSource messageSource;

    public UserInfoController(MessageSource messageSource) {
        this.messageSource = messageSource;
    }

    @GetMapping("/info")
    public Map<String, Object> info(HttpServletRequest request, Locale locale) {
        String ip = clientIp(request);

        Map<String, Object> result = new LinkedHashMap<>();
        result.put("ip", ip);
        result.put("locale", locale.toString());
        result.put("message", greeting(locale));

        Map<String, Object> geo = geoLookup(ip);
        result.put("lat", geo.get("lat"));
        result.put("lon", geo.get("lon"));

        return result;
    }

    private String greeting(Locale locale) {
        return messageSource.getMessage("greeting", null, "Hello!", locale);
    }

    private String clientIp(HttpServletRequest request) {
        String forwardedFor = request.getHeader("X-Forwarded-For");
        if (forwardedFor != null && !forwardedFor.isBlank()) {
            return forwardedFor.split(",")[0].trim();
        }
        return request.getRemoteAddr();
    }

    @SuppressWarnings("unchecked")
    private Map<String, Object> geoLookup(String ip) {
        Map<String, Object> empty = new LinkedHashMap<>();
        empty.put("lat", null);
        empty.put("lon", null);

        // localhost/private IPs have no public geolocation
        if (ip == null || ip.equals("127.0.0.1") || ip.equals("0:0:0:0:0:0:0:1")) {
            return empty;
        }
        try {
            Map<String, Object> body = restClient.get()
                    .uri("http://ip-api.com/json/{ip}?fields=lat,lon", ip)
                    .retrieve()
                    .body(Map.class);
            return body != null ? body : empty;
        } catch (Exception e) {
            return empty;
        }
    }
}
