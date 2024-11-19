package com.example.interfaces;

import lombok.AllArgsConstructor;
import lombok.NoArgsConstructor;
import org.springframework.stereotype.Component;

import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;
import java.util.Scanner;
import java.time.LocalDate;

@AllArgsConstructor
@NoArgsConstructor

@Component
public class InterfazRankingVinos {

    private LocalDate fechaDesdeSeleccionada;
    private LocalDate fechaHastaSeleccionada;
    private String tipoReseñaSeleccionada;
    private String tipoVisualizacionSeleccionado;
    private boolean confirmacionGeneracionReporte;

    public void habilitar() {
        System.out.println("Pantalla habilitada!");
    }

    public void solicitarFechaDesdeYHasta() {
        System.out.println("Ingrese la fecha Desde y Fecha Hasta.");
    }

    public LocalDate tomarFechaDesde(String fechaDesdeIngresada) {
        LocalDate fechaDesde = null;

        try {
            DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");
            fechaDesde = LocalDate.parse(fechaDesdeIngresada, formatter);

            // Si la fecha es válida, se almacena en la variable de instancia
            this.fechaDesdeSeleccionada = fechaDesde;

        } catch (DateTimeParseException e) {
            System.out.println("Formato de fecha inválido. Por favor, utiliza el formato yyyy-MM-dd.");
            // Aquí puedes lanzar una excepción o manejar el error como desees
        }
        return fechaDesde;
    }

    public LocalDate tomarFechaHasta(String fechaHastaIngresada) {
        LocalDate fechaHasta = null;

        try {
            DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");
            fechaHasta = LocalDate.parse(fechaHastaIngresada, formatter);

            // Si la fecha es válida, se almacena en la variable de instancia
            this.fechaHastaSeleccionada = fechaHasta;

        } catch (DateTimeParseException e) {
            System.out.println("Formato de fecha inválido. Por favor, utiliza el formato yyyy-MM-dd.");
            // Aquí puedes lanzar una excepción o manejar el error como desees
        }
        return fechaHasta;
    }

    public boolean validarPeriodo(LocalDate fechaDesde, LocalDate fechaHasta) {
        return !fechaDesde.isAfter(fechaHasta);
    }

    public void solicitarTipoReseña() {

        System.out.println("Ingrese el tipo de reseña.");
    }

    public String tomarTipoReseña(String tipoReseña) {
        String[] opcionesValidas = {"premium", "amigo", "normal"};

        String tipoSeleccionado = tipoReseña.toLowerCase();

        for (String opcion : opcionesValidas) {
            if (tipoSeleccionado.equals(opcion)) {
                this.tipoReseñaSeleccionada = tipoSeleccionado;
                return this.tipoReseñaSeleccionada;
            }
        }
        System.out.println("Opción inválida. Por favor, elige entre premium, amigo o normal.");
        return null;
    }

    public void solicitarTipoVisualizacion() {

        System.out.println("Ingrese el tipo de visualizacion");
    }

    public String tomarTipoVisualizacion(String tipoVisualizacion) {
        String[] opcionesValidas = {"pdf", "excel", "pantalla"};
        String tipoSeleccionado = tipoVisualizacion.toLowerCase();

        System.out.println("Tipo recibido: " + tipoSeleccionado);
        boolean esValido = false;

        for (String opcion : opcionesValidas) {
            if (tipoSeleccionado.equals(opcion)) {
                this.tipoVisualizacionSeleccionado = tipoSeleccionado;
                esValido = true;
                break;
            }
        }
        return this.tipoVisualizacionSeleccionado;
    }

    public void solicitarConfirmacionGeneracionReporte() {

        System.out.println("Desea confirmar?");
    }

    public boolean tomarConfirmacionGeneracionReporte(String confirmacion) {

        if (confirmacion == "true") {
            this.confirmacionGeneracionReporte = true;
            return true;
        } else {
            this.confirmacionGeneracionReporte = false;
            return false;
        }
    }
}