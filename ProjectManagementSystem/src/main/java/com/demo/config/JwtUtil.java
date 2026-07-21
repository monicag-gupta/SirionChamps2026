package com.demo.config;


import java.util.Date;

import javax.crypto.SecretKey;

import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Component;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;

@Component
public class JwtUtil {

    private static final String SECRET =
            "mySecretKeyForProjectManagementSystemJWTAuthentication123456789";

    private final SecretKey key = Keys.hmacShaKeyFor(SECRET.getBytes());

    private static final long EXPIRATION = 1000 * 60 * 60;

    public String generateToken(String username) {

        return Jwts.builder()
                .subject(username)
                .issuedAt(new Date())
                .expiration(new Date(System.currentTimeMillis() + EXPIRATION))
                .signWith(key)
                .compact();
    }

    public String extractUsername(String token) {

        return getClaims(token).getSubject();
    }

    public boolean validateToken(String token,
                                 UserDetails userDetails) {

        return extractUsername(token)
                .equals(userDetails.getUsername())
                && !isExpired(token);
    }

    private boolean isExpired(String token) {

        return getClaims(token)
                .getExpiration()
                .before(new Date());
    }

    private Claims getClaims(String token) {

        return Jwts.parser()
                .verifyWith(key)
                .build()
                .parseSignedClaims(token)
                .getPayload();
    }
}