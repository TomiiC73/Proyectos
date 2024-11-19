package com.example.services;

import com.example.dto.InputDTO;
import com.example.entidades.*;
import com.example.repositorios.VinoRepository;
import com.example.gestor.GestorRankingVinos;
import com.example.interfaces.InterfazRankingVinos;
import org.springframework.stereotype.Component;
import org.springframework.stereotype.Service;
import org.springframework.beans.factory.annotation.Autowired;
import java.io.IOException;
import java.time.LocalDate;
import java.util.List;

@Service
@Component
public class ReporteService {

    private final VinoRepository vinoRepository;
    private final GestorRankingVinos gestorRankingVinos;
    private final InterfazRankingVinos interfazRankingVinos;

    @Autowired
    public ReporteService(VinoRepository vinoRepository, GestorRankingVinos gestorRankingVinos,
                          InterfazRankingVinos interfazRankingVinos) {
        this.vinoRepository = vinoRepository;
        this.gestorRankingVinos = gestorRankingVinos;
        this.interfazRankingVinos = interfazRankingVinos;
    }

    public void generarReporte(InputDTO inputDTO) throws IOException {
        List<Vino> vinos = vinoRepository.findAll();
        Vino[] arregloDeVinos = vinos.toArray(new Vino[0]);

        interfazRankingVinos.habilitar();
        gestorRankingVinos.opcionGenerarRankingVinos();
        LocalDate fechaDesde = interfazRankingVinos.tomarFechaDesde(inputDTO.getFechaDesde());
        LocalDate fechaHasta = interfazRankingVinos.tomarFechaHasta(inputDTO.getFechaHasta());

        interfazRankingVinos.validarPeriodo(fechaDesde, fechaHasta);
        gestorRankingVinos.tomarFechaDesdeYHasta(fechaDesde, fechaHasta);

        String tipoReseña = interfazRankingVinos.tomarTipoReseña(inputDTO.getTipoReseña());
        gestorRankingVinos.tomarTipoReseña(tipoReseña);

        String tipoVisualizacion = interfazRankingVinos.tomarTipoVisualizacion(inputDTO.getTipoVisualizacion());
        gestorRankingVinos.tomarTipoVisualizacion(tipoVisualizacion);

        boolean confirmacion = interfazRankingVinos.tomarConfirmacionGeneracionReporte(inputDTO.getConfirmacion());
        gestorRankingVinos.tomarConfirmacionGenerarReporte(confirmacion);

        List<String[]> vinosFiltrados = gestorRankingVinos.buscarVinosConReseñaEnPeriodo(arregloDeVinos, new LocalDate[]{fechaDesde, fechaHasta});
        List<String[]> vinosOrdenados = gestorRankingVinos.ordenarVinos(vinosFiltrados);

        if ("excel".equals(tipoVisualizacion)) {
            gestorRankingVinos.exportarExcel(vinosOrdenados);
        }
        if ("pdf".equals(tipoVisualizacion)) {
            gestorRankingVinos.exportarPDF(vinosOrdenados);
        }
    }
}