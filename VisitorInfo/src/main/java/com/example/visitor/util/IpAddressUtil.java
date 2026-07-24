package com.example.visitor.util;

import jakarta.servlet.http.HttpServletRequest;

public class IpAddressUtil {

    public static String getClientIp(HttpServletRequest request) {

        String ip = request.getHeader("X-Forwarded-For");

        if (ip != null && !ip.isBlank()) {
            return ip.split(",")[0];
        }

        ip = request.getHeader("X-Real-IP");

        if (ip != null && !ip.isBlank()) {
            return ip;
        }

        return request.getRemoteAddr();
    }
}
