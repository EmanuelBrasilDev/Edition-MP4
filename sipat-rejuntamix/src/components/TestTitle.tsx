import {interpolate, useCurrentFrame, useVideoConfig} from 'remotion';

export const TestTitle = () => {
  const frame = useCurrentFrame();
  const {fps, width} = useVideoConfig();
  return (
    <div style={{
      opacity: interpolate(frame, [0, fps / 2], [0, 1], {extrapolateRight: 'clamp'}),
      textAlign: 'center', padding: width * 0.08, fontFamily: 'Arial, sans-serif',
    }}>
      <div style={{color: '#f58220', fontSize: width * 0.065, fontWeight: 700}}>TESTE TÉCNICO</div>
      <div style={{color: '#fff', fontSize: width * 0.032, marginTop: 30}}>SIPAT · RejuntaMix</div>
      <div style={{color: '#fff', fontSize: width * 0.022, marginTop: 30}}>Material sintético · sem edição final</div>
    </div>
  );
};
