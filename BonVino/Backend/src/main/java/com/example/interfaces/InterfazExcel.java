package com.example.interfaces;

import lombok.*;
import org.apache.poi.ss.usermodel.Workbook;
import org.apache.poi.ss.usermodel.*;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import org.springframework.stereotype.Component;

import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.file.Paths;
import java.util.List;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Component
public class InterfazExcel {

    private String nombre;
    private String calificacion;
    private String precioSugerido;
    private String nombreBodega;
    private String varietal;
    private String region;
    private String pais;

    // Metodo para crear el Excel a partir de una lista de resultados
    public void exportarExcel(List<String[]> datos) throws IOException {
        Workbook workbook = new XSSFWorkbook();
        Sheet sheet = workbook.createSheet("Vinos");

        // Crear estilo para encabezados
        CellStyle encabezadoStyle = workbook.createCellStyle();
        encabezadoStyle.setFillForegroundColor(IndexedColors.RED.getIndex()); // Color de fondo
        encabezadoStyle.setFillPattern(FillPatternType.SOLID_FOREGROUND);

        Font font = workbook.createFont();
        font.setColor(IndexedColors.WHITE.getIndex()); // Color de la fuente
        font.setBold(true); // Negrita
        encabezadoStyle.setFont(font);

        // Crear encabezados
        Row encabezados = sheet.createRow(0);
        encabezados.createCell(0).setCellValue("Nombre");
        encabezados.createCell(1).setCellValue("Calificación");
        encabezados.createCell(2).setCellValue("Precio Sugerido");
        encabezados.createCell(3).setCellValue("Nombre Bodega");
        encabezados.createCell(4).setCellValue("Varietal");
        encabezados.createCell(5).setCellValue("Región");
        encabezados.createCell(6).setCellValue("País");

        // Llenar los datos
        int fila = 1;
        for (String[] infoVino : datos) {
            Row filaDatos = sheet.createRow(fila++);
            filaDatos.createCell(0).setCellValue(infoVino[0]); // Nombre
            filaDatos.createCell(1).setCellValue(infoVino[1]); // Calificación
            filaDatos.createCell(2).setCellValue(infoVino[2]); // Precio Sugerido
            filaDatos.createCell(3).setCellValue(infoVino[3]); // Nombre Bodega
            filaDatos.createCell(4).setCellValue(infoVino[4]); // Varietal
            filaDatos.createCell(5).setCellValue(infoVino[5]); // Región
            filaDatos.createCell(6).setCellValue(infoVino[6]); // País
        }

        String nombreArchivo = "ReporteRankingVinos.xlsx";
        String rutaArchivo = Paths.get(System.getProperty("user.dir"), nombreArchivo).toString();

        // Escribir el archivo
        try (FileOutputStream fileOut = new FileOutputStream(rutaArchivo)) {
            workbook.write(fileOut);
            System.out.println("Excel creado exitosamente en: " + rutaArchivo);
        } catch (IOException e) {
            throw new RuntimeException(e);
        } finally {
            workbook.close();
        }
    }
}