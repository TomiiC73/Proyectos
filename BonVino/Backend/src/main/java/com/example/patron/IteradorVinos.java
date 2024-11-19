package com.example.patron;

import com.example.entidades.Vino;

import java.time.LocalDate;

public class IteradorVinos implements IIterador {

    private Object[] vinos;
    private LocalDate[] filtros;
    private int posicion;

    public IteradorVinos(Object[] vinos, LocalDate[] filtros) {
        this.vinos = vinos;
        this.filtros = filtros;
    }

    @Override
    public void primero() {
        posicion = 0;
    }

    @Override
    public boolean haTerminado() {
        if (vinos.length == posicion) return true;
        else return false;
    }

    @Override
    public Object actual() {
        return vinos[posicion];
    }

    @Override
    public boolean cumpleFiltro(Object elemento, LocalDate[] filtro) {
        return true;
    }

    @Override
    public void siguiente() {
        if (!haTerminado()) {
            posicion ++;
        }
    }
}
