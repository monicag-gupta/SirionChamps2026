package com.demo.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import com.demo.entity.Project;
import com.demo.service.ProjectService;

@RestController
@RequestMapping("/projects")
public class ProjectController {

    @Autowired
    private ProjectService service;

    @PostMapping
    public Project save(@RequestBody Project project) {

        return service.save(project);
    }

    @GetMapping
    public List<Project> getAll() {

        return service.getAllProjects();
    }

    @GetMapping("/{id}")
    public Project getProject(@PathVariable Long id) {

        return service.getProject(id).orElse(null);
    }

    @PutMapping("/{id}")
    public Project update(@PathVariable Long id,
                          @RequestBody Project project) {

        project.setPid(id);

        return service.update(project);
    }

    @DeleteMapping("/{id}")
    public String delete(@PathVariable Long id) {

        service.delete(id);

        return "Project Deleted Successfully";
    }

}