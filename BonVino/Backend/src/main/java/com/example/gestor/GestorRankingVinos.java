package com.example.gestor;

import com.example.entidades.Vino;
import com.example.interfaces.InterfazExcel;
import com.example.interfaces.InterfazPDF;
import com.example.interfaces.InterfazRankingVinos;
import com.example.patron.IAgregado;
import com.example.patron.IIterador;
import com.example.patron.IteradorVinos;
import lombok.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Component
public class GestorRankingVinos implements IAgregado {

    private LocalDate fechaDesdeSeleccionada;
    private LocalDate fechaHastaSeleccionada;
    private String tipoReseñaSeleccionada;
    private String tipoVisualizacionSeleccionado;
    private boolean confirmacionGeneracionReporte;
    private Vino[] vinos;

    private InterfazRankingVinos interfazRankingVinos;
    private InterfazExcel interfazExcel;
    private InterfazPDF interfazPDF;

    @Autowired
    public GestorRankingVinos(InterfazRankingVinos interfazRankingVinos, InterfazExcel interfazExcel, InterfazPDF interfazPDF) {
        this.interfazRankingVinos = interfazRankingVinos;
        this.interfazExcel = interfazExcel;
        this.interfazPDF = interfazPDF;
    }

    @Override
    public IIterador crearIterador(Object[] elementos, LocalDate[] fechas) {

        IIterador iterador = new IteradorVinos(elementos, fechas);
        return iterador;
    }

    public void opcionGenerarRankingVinos() {
        interfazRankingVinos.solicitarFechaDesdeYHasta();
    }

    public void tomarFechaDesdeYHasta(LocalDate fechaDesde, LocalDate fechaHasta) {
        this.fechaDesdeSeleccionada = fechaDesde;
        this.fechaHastaSeleccionada = fechaHasta;

        interfazRankingVinos.solicitarTipoReseña();
    }

    public void tomarTipoReseña(String tipoReseña) {

        this.tipoReseñaSeleccionada = tipoReseña;
        System.out.println("Tipo de reseña seleccionada: " + this.tipoReseñaSeleccionada);

        interfazRankingVinos.solicitarTipoVisualizacion();
    }

    public void tomarTipoVisualizacion(String tipoVisualizacion) {
        this.tipoVisualizacionSeleccionado = tipoVisualizacion;

        interfazRankingVinos.solicitarConfirmacionGeneracionReporte();
    }

    public void tomarConfirmacionGenerarReporte(boolean confirmacion) {
        this.confirmacionGeneracionReporte = confirmacion;
    }

    public Double calcularPorcentajeDeSomelierEnPeriodo(LocalDate[] fechas, Vino vino) {
        Double acumulador = 0.0;
        int contador = 0;
        LocalDate fechaDesde = fechas[0];
        LocalDate fechaHasta = fechas[1];

        Double promedio = vino.calcularPorcentajeDeSomelierEnPeriodo(fechaDesde, fechaHasta);

        if (promedio != null) {
            acumulador += promedio;
            contador++;
        }

        // Calcular el promedio
        promedio = contador > 0 ? acumulador / contador : 0.0;
        return promedio;
    }
    
    public List<String[]> buscarVinosConReseñaEnPeriodo(Vino[] vinos, LocalDate[] filtros) {
        IIterador iteradorVinos = this.crearIterador(vinos, filtros);
        iteradorVinos.primero();

        // Lista para almacenar los resultados
        List<String[]> resultados = new ArrayList<>();

        while (!iteradorVinos.haTerminado()) {
            Vino vino = (Vino) iteradorVinos.actual();

            if (iteradorVinos.cumpleFiltro(vino, filtros) && vino.tenesReseñasEnPeriodo(filtros)) {
                String[] infoVino = new String[7]; // Array para almacenar los datos
                infoVino[0] = vino.getNombre();
                infoVino[1] = String.valueOf(this.calcularPorcentajeDeSomelierEnPeriodo(filtros, vino));
                infoVino[2] = String.valueOf(vino.getPrecio());
                infoVino[3] = vino.getBodega().getNombre();
                infoVino[4] = vino.getVarietal().getDescripcion();
                infoVino[5] = vino.getBodega().getRegionVitivinicolaBodega().getNombre();
                infoVino[6] = vino.getBodega().getRegionVitivinicolaBodega().obtenerPais();

                // Agregar el array de información a la lista de resultados
                resultados.add(infoVino);
            }
            iteradorVinos.siguiente();
        }
        return resultados;
    }

    public List<String[]> ordenarVinos(List<String[]> vinos) {
        vinos.sort((a, b) -> Double.compare(Double.parseDouble(b[1]), Double.parseDouble(a[1])));

        if (vinos.size() > 10) {
            vinos = vinos.subList(0, 10);
        }
        return vinos;
    }

    public void exportarExcel(List<String[]> resultados) throws IOException {
        interfazExcel.exportarExcel(resultados);
    }

    public void exportarPDF(List<String[]> resultados) throws IOException {
        interfazPDF.exportarPDF(resultados);
    }

    public void finCU() {}
}