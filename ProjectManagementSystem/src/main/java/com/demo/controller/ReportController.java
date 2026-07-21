package com.demo.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import com.demo.entity.Employee;
import com.demo.entity.Project;
import com.demo.entity.Skill;
import com.demo.entity.Team;
import com.demo.service.ProjectService;

@RestController
@RequestMapping("/reports")
public class ReportController {

    @Autowired
    private ProjectService service;

    @GetMapping("/projectCount")
    public long projectCount() {

        return service.projectCount();
    }

    @GetMapping("/manager/{name}")
    public List<Project> projectByManager(@PathVariable String name) {

        return service.projectsByManager(name);
    }

    @GetMapping("/language/{language}")
    public List<Project> projectByLanguage(@PathVariable String language) {

        return service.projectsByLanguage(language);
    }

    @GetMapping("/employees")
    public List<Employee> employees() {

        return service.allEmployees();
    }

    @GetMapping("/skills")
    public List<Skill> skills() {

        return service.allSkills();
    }

    @GetMapping("/team/{pid}")
    public List<Team> team(@PathVariable Long pid) {

        return service.employeesInProject(pid);
    }

}