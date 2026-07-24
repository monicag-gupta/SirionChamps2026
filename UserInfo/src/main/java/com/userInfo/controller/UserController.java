package com.userInfo.controller;

import com.userInfo.model.LocationRequest;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Locale;
import java.util.Map;

@RestController
public class UserController {

    @GetMapping("/info")
    public Map<String, Object> getInfo(HttpServletRequest request,
                                       Locale locale) {

        Map<String, Object> map = new HashMap<>();

        map.put("IP Address", request.getRemoteAddr());
        map.put("Locale", locale.toString());
        map.put("Language", locale.getLanguage());
        map.put("Country", locale.getCountry());
        map.put("User Agent", request.getHeader("User-Agent"));

        return map;
    }

    @PostMapping("/location")
    public Map<String, Object> location(@RequestBody LocationRequest location,
                                        HttpServletRequest request,
                                        Locale locale) {

        Map<String, Object> map = new HashMap<>();

        map.put("IP Address", request.getRemoteAddr());
        map.put("Locale", locale.toString());
        map.put("Latitude", location.getLatitude());
        map.put("Longitude", location.getLongitude());
        map.put("User Agent", request.getHeader("User-Agent"));

        System.out.println(map);

        return map;
    }

}