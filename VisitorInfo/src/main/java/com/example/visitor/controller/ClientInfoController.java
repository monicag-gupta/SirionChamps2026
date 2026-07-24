package com.example.visitor.controller;

import java.util.Locale;

import org.springframework.web.bind.annotation.*;

import com.example.visitor.service.ClientInfoService;

import jakarta.servlet.http.HttpServletRequest;

@RestController
public class ClientInfoController {

	private final ClientInfoService service;

	public ClientInfoController(ClientInfoService service) {
		this.service = service;
	}

	@PostMapping("/api/client-info")
	public String getInfo(HttpServletRequest request, Locale locale) {

		return service.getInfo(request, locale);
	}

}
