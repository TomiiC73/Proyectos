package com.example.patron;

import java.time.LocalDate;

public interface IIterador {

    public Object actual();
    public boolean cumpleFiltro(Object elemento, LocalDate[] filtro);
    public boolean haTerminado();
    public void primero();
    public void siguiente();
}