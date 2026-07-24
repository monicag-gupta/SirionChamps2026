package com.example.visitor.util;

import nl.basjes.parse.useragent.UserAgentAnalyzer;

public class UserAgentParserUtil {

	private static final UserAgentAnalyzer analyzer = UserAgentAnalyzer.newBuilder().hideMatcherLoadStats()
			.withField("AgentName").withField("AgentVersion").withField("OperatingSystemName").withField("DeviceClass")
			.build();

	public static String parse(String ua) {

		var result = analyzer.parse(ua);

		return """
				Browser : %s %s
				OS : %s
				Device : %s
				""".formatted(result.getValue("AgentName"), result.getValue("AgentVersion"),
				result.getValue("OperatingSystemName"), result.getValue("DeviceClass"));
	}

}
