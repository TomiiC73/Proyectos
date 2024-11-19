package com.example.patron;

import com.example.entidades.Reseña;
import lombok.AllArgsConstructor;
import lombok.NoArgsConstructor;

import java.time.LocalDate;

@NoArgsConstructor
@AllArgsConstructor
public class IteradorReseñas implements IIterador{

    private Reseña[] reseñas;
    private LocalDate[] filtro;
    private int posicion = 0;

    public IteradorReseñas(Reseña[] reseñas, LocalDate[] filtro) {
        this.reseñas = reseñas;
        this.filtro = filtro;
    }

    @Override
    public void primero() {

        posicion = 0;
    }

    @Override
    public Reseña actual() {

        return reseñas[posicion];
    }

    @Override
    public boolean cumpleFiltro(Object object, LocalDate[] filtro) {

        Reseña reseña = (Reseña) object;
        LocalDate fechaDesde = filtro[0];
        LocalDate fechaHasta = filtro[1];

        if (reseña.sosDeSomelier() && reseña.sosDePeriodo(fechaDesde, fechaHasta)) {
            return true;
        } else {
            return false;
        }
    }

    @Override
    public boolean haTerminado() {
        if (reseñas.length == posicion) return true;
        else return false;
    }

    @Override
    public void siguiente() {
        if (!haTerminado()) {
            posicion ++;
        }
    }
}