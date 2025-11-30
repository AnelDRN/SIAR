import { render, screen } from '@testing-library/react';
import InfoPanel from './InfoPanel';

describe('InfoPanel', () => {
  it('renders the initial message when no polygon is selected', () => {
    render(<InfoPanel selectedPolygon={null} analysisStatus="idle" onStartAnalysis={() => {}} />);
    expect(screen.getByText('Draw a polygon on the map to start.')).toBeInTheDocument();
  });
});
