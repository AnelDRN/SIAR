import React, { useEffect, useState } from 'react';
import { useMap, FeatureGroup } from 'react-leaflet';
import L from 'leaflet';
import { useDrawControl } from '../hooks/useDrawControl';

interface DrawControlLayerProps {
  onPolygonCreated: (layer: L.Layer) => void;
  onClear: () => void;
  selectedPolygon: any;
}

const DrawControlLayer: React.FC<DrawControlLayerProps> = ({ onPolygonCreated, onClear, selectedPolygon }) => {
  const map = useMap();
  const [featureGroup, setFeatureGroup] = useState<L.FeatureGroup | null>(null);

  useDrawControl({
    map,
    featureGroup,
    onPolygonCreated,
    onClear,
  });

  useEffect(() => {
    // This effect handles clearing the layers when the parent component nullifies the selection.
    // It no longer tries to re-add layers, as that conflicts with the useDrawControl hook.
    if (!selectedPolygon && featureGroup) {
      featureGroup.clearLayers();
    }
  }, [selectedPolygon, featureGroup]);

  return <FeatureGroup ref={(ref) => setFeatureGroup(ref)} />;
};

export default DrawControlLayer;
