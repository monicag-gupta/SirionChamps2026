package com.demo.service;

import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.demo.entity.Employee;
import com.demo.entity.Project;
import com.demo.entity.Skill;
import com.demo.entity.Team;
import com.demo.repository.EmployeeRepository;
import com.demo.repository.ProjectRepository;
import com.demo.repository.SkillRepository;
import com.demo.repository.TeamRepository;

@Service
public class ProjectService {

    @Autowired
    private ProjectRepository projectRepository;

    @Autowired
    private EmployeeRepository employeeRepository;

    @Autowired
    private SkillRepository skillRepository;

    @Autowired
    private TeamRepository teamRepository;

    //---------------- PROJECT CRUD ----------------//

    public Project save(Project project) {
        return projectRepository.save(project);
    }

    public List<Project> getAllProjects() {
        return projectRepository.findAll();
    }

    public Optional<Project> getProject(Long id) {
        return projectRepository.findById(id);
    }

    public Project update(Project project) {
        return projectRepository.save(project);
    }

    public void delete(Long id) {
        projectRepository.deleteById(id);
    }

    //---------------- REPORTS ----------------//

    public long projectCount() {
        return projectRepository.count();
    }

    public List<Project> projectsByManager(String manager) {
        return projectRepository.findByPmngr(manager);
    }

    public List<Project> projectsByLanguage(String language) {
        return projectRepository.findByLanguage(language);
    }

    public List<Employee> allEmployees() {
        return employeeRepository.findAll();
    }

    public List<Skill> allSkills() {
        return skillRepository.findAll();
    }

    public List<Team> employeesInProject(Long pid) {
        return teamRepository.findByProjectPid(pid);
    }

}