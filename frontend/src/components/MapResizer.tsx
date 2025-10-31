import { useEffect } from 'react';
import { useMap } from 'react-leaflet';

const MapResizer: React.FC = () => {
  const map = useMap();

  useEffect(() => {
    map.invalidateSize();
  }, [map]);

  return null;
};

export default MapResizer;
