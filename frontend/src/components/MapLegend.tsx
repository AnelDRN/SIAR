import React, { useEffect } from 'react';
import { useMap } from 'react-leaflet';
import L from 'leaflet';
import './MapLegend.css';

const MapLegend: React.FC = () => {
  const map = useMap();

  useEffect(() => {
    const legend = new L.Control({ position: 'bottomright' });

    legend.onAdd = () => {
      const div = L.DomUtil.create('div', 'info legend');
      const grades = [
        { level: 'HIGH', color: '#2e7d32', label: 'Alta' },
        { level: 'MEDIUM', color: '#ed6c02', label: 'Media' },
        { level: 'LOW', color: '#d32f2f', label: 'Baja' },
      ];
      let labels = '<strong>Viabilidad</strong><br>';
      
      grades.forEach(grade => {
        labels += `<i style="background:${grade.color}"></i> ${grade.label}<br>`;
      });

      div.innerHTML = labels;
      return div;
    };

    legend.addTo(map);

    return () => {
      legend.remove();
    };
  }, [map]);

  return null;
};

export default MapLegend;
