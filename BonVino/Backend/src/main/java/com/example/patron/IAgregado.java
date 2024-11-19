package com.example.patron;

import java.time.LocalDate;

public interface IAgregado {

    IIterador crearIterador(Object[] elementos, LocalDate[] fechas);
}
