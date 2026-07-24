package com.example.visitor.service;

import java.util.Locale;

import org.springframework.context.MessageSource;
import org.springframework.stereotype.Service;

import com.example.visitor.util.IpAddressUtil;
import com.example.visitor.util.UserAgentParserUtil;

import jakarta.servlet.http.HttpServletRequest;

@Service
public class ClientInfoService {

	private final MessageSource messageSource;

	public ClientInfoService(MessageSource messageSource) {
		this.messageSource = messageSource;
	}

	public String getInfo(HttpServletRequest request, Locale locale) {

		String ip = IpAddressUtil.getClientIp(request);

		String ua = request.getHeader("User-Agent");

		String browser = UserAgentParserUtil.parse(ua);

		String language = request.getHeader("Accept-Language");

		String welcome = messageSource.getMessage("welcome", null, locale);

		return """
				==============================

				%s

				IP Address : %s

				Locale : %s

				Accept-Language :
				%s

				%s

				==============================
				""".formatted(welcome, ip, locale, language, browser);

	}

}
