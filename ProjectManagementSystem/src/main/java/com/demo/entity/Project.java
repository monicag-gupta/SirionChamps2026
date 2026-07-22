package com.demo.entity;

import jakarta.persistence.*;

@Entity
@Table(name = "projects")
public class Project {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long pid;

    private String pname;

    private int duration;

    private String pmngr;

    // Changed from pLanguage to language
    private String language;

    public Project() {
    }

    public Project(Long pid, String pname, int duration, String pmngr, String language) {
        this.pid = pid;
        this.pname = pname;
        this.duration = duration;
        this.pmngr = pmngr;
        this.language = language;
    }

    public Long getPid() {
        return pid;
    }

    public void setPid(Long pid) {
        this.pid = pid;
    }

    public String getPname() {
        return pname;
    }

    public void setPname(String pname) {
        this.pname = pname;
    }

    public int getDuration() {
        return duration;
    }

    public void setDuration(int duration) {
        this.duration = duration;
    }

    public String getPmngr() {
        return pmngr;
    }

    public void setPmngr(String pmngr) {
        this.pmngr = pmngr;
    }

    public String getLanguage() {
        return language;
    }

    public void setLanguage(String language) {
        this.language = language;
    }
}