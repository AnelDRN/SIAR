import { useEffect } from 'react';
import L from 'leaflet';
import 'leaflet-draw';

interface UseDrawControlOptions {
  map: L.Map | null;
  featureGroup: L.FeatureGroup | null;
  onPolygonCreated: (layer: L.Layer) => void;
  onClear: () => void;
}

export const useDrawControl = ({ map, featureGroup, onPolygonCreated, onClear }: UseDrawControlOptions) => {
  useEffect(() => {
    if (!map || !featureGroup) return;

    const drawControl = new L.Control.Draw({
      draw: {
        polygon: true,
        polyline: false,
        circle: false,
        rectangle: true,
        marker: false,
        circlemarker: false,
      },
      edit: {
        featureGroup: featureGroup,
        remove: true,
      },
    });

    map.addControl(drawControl);

    const handleCreated = (event: L.DrawEvents.Created) => {
      if (featureGroup) {
        // Clear previous layers before adding the new one
        featureGroup.clearLayers();
        // Add the newly drawn layer to the feature group so it's visible
        featureGroup.addLayer(event.layer);
      }
      // Notify the parent component with the new layer's data
      onPolygonCreated(event.layer);
    };

    const handleDeleted = () => {
      onClear();
    };

    map.on(L.Draw.Event.CREATED, handleCreated);
    map.on(L.Draw.Event.DELETED, handleDeleted);

    return () => {
      map.removeControl(drawControl);
      map.off(L.Draw.Event.CREATED, handleCreated);
      map.off(L.Draw.Event.DELETED, handleDeleted);
    };
  }, [map, featureGroup, onPolygonCreated, onClear]);
};
