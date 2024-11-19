package com.example.controllers;

import com.example.dto.InputDTO;
import com.example.services.ReporteService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import java.io.IOException;

@Slf4j
@RestController
@RequestMapping("/vinos")
@CrossOrigin(origins = "http://localhost:3000")

public class ReporteController {

    @Autowired
    private ReporteService reporteService;

    @PostMapping("/reporte-ranking-vinos")
    public String generarRankingVinos(@RequestBody InputDTO inputDTO) throws IOException {

        try {
            reporteService.generarReporte(inputDTO);
            return "Reporte generado exitosamente.";

        } catch (IOException e) {
            log.error("Error al generar el reporte: {}", e.getMessage());
            return "Error al generar el reporte.";
        }
    }
}