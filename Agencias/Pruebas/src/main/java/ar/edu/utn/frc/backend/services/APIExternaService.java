package ar.edu.utn.frc.backend.services;

import ar.edu.utn.frc.backend.dtosApiExterna.DTOPosicionAPI;
import lombok.extern.slf4j.Slf4j;
import org.hibernate.service.spi.ServiceException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Slf4j
@Service
public class APIExternaService {

    private RestTemplate restTemplate;

    @Autowired
    public APIExternaService(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    public DTOPosicionAPI getConfiguracionAPI() throws ServiceException {
        try {
            String apiUrl = "https://labsys.frc.utn.edu.ar/apps-disponibilizadas/backend/api/v1/configuracion/";
            return restTemplate.getForObject(apiUrl, DTOPosicionAPI.class);

        } catch (Exception e) {
            log.error("Error al obtener configuracion API", e);
            return null;
        }
    }
}