package com.example.dto;

import lombok.*;

@Data
@NoArgsConstructor
@AllArgsConstructor

public class InputDTO {
    private String fechaDesde;
    private String fechaHasta;
    private String tipoReseña;
    private String tipoVisualizacion;
    private String confirmacion;
}