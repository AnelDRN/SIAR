import { renderHook, act } from '@testing-library/react';
import axios from 'axios';
import { useAnalysis } from './useAnalysis';

vi.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

const geoJSON = {
  type: 'Feature',
  geometry: {
    type: 'Polygon',
    coordinates: [
      [
        [-74, 4],
        [-73.9, 4],
        [-73.9, 3.9],
        [-74, 3.9],
        [-74, 4],
      ],
    ],
  },
  properties: {},
};

describe('useAnalysis Hook', () => {
  beforeEach(() => {
    vi.useFakeTimers();
    mockedAxios.post.mockClear();
    mockedAxios.get.mockClear();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it('should have correct initial state', () => {
    const { result } = renderHook(() => useAnalysis());
    expect(result.current.analysisStatus).toBe('idle');
    expect(result.current.analysisResults).toBeNull();
  });

  it('should handle successful analysis request and polling', async () => {
    const { result } = renderHook(() => useAnalysis());

    // Mock the initial POST request
    mockedAxios.post.mockResolvedValue({ data: { id: 123, properties: {} } });
    
    // Mock the polling GET request for status
    mockedAxios.get.mockResolvedValueOnce({ data: { properties: { status: 'PENDING' } } });
    mockedAxios.get.mockResolvedValueOnce({ data: { properties: { status: 'COMPLETED' } } });
    
    // Mock the final GET request for results
    mockedAxios.get.mockResolvedValueOnce({ data: { features: [] } });

    // Start the analysis
    await act(async () => {
      result.current.startAnalysis(geoJSON);
    });

    // At this point, the status should be loading
    expect(result.current.analysisStatus).toBe('loading');
    expect(mockedAxios.post).toHaveBeenCalledTimes(1);

    // Fast-forward timers to trigger the first poll
    await act(async () => {
        vi.advanceTimersByTime(3000);
    });
    
    // Fast-forward timers to trigger the second poll
    await act(async () => {
        vi.advanceTimersByTime(3000);
    });

    // Now the status should be success and the results should be set
    expect(result.current.analysisStatus).toBe('success');
    expect(result.current.analysisResults).toEqual({ features: [] });
    expect(mockedAxios.get).toHaveBeenCalledTimes(3); // 1 for pending, 1 for completed, 1 for results
  });

  it('should handle failed analysis request', async () => {
    const { result } = renderHook(() => useAnalysis());

    // Mock the initial POST request to fail
    mockedAxios.post.mockRejectedValue(new Error('Network Error'));

    await act(async () => {
      result.current.startAnalysis(geoJSON);
    });

    expect(result.current.analysisStatus).toBe('error');
  });

  it('should handle polling failure', async () => {
    const { result } = renderHook(() => useAnalysis());
    mockedAxios.post.mockResolvedValue({ data: { id: 123, properties: {} } });
    mockedAxios.get.mockRejectedValue(new Error('Polling Error'));

    await act(async () => {
      result.current.startAnalysis(geoJSON);
    });

    await act(async () => {
        vi.advanceTimersByTime(3000);
    });

    expect(result.current.analysisStatus).toBe('error');
  });

  it('should handle analysis failure on backend', async () => {
    const { result } = renderHook(() => useAnalysis());
    mockedAxios.post.mockResolvedValue({ data: { id: 123, properties: {} } });
    mockedAxios.get.mockResolvedValue({ data: { properties: { status: 'FAILED' } } });

    await act(async () => {
      result.current.startAnalysis(geoJSON);
    });

    await act(async () => {
        vi.advanceTimersByTime(3000);
    });

    expect(result.current.analysisStatus).toBe('error');
  });
});
