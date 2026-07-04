import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import App from './App';

test('renders the PokeSim app shell', () => {
  render(
    <MemoryRouter>
      <App />
    </MemoryRouter>
  );
  const brand = screen.getByText(/PokeSim/i);
  expect(brand).toBeInTheDocument();
});
