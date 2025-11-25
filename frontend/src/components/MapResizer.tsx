import { useEffect } from 'react';
import { useMap } from 'react-leaflet';

const MapResizer: React.FC = () => {
  const map = useMap();

  useEffect(() => {
    const timer = setTimeout(() => {
      map.invalidateSize();
    }, 100);

    // Cleanup the timer if the component unmounts
    return () => clearTimeout(timer);
  }, [map]);

  return null;
};

export default MapResizer;
