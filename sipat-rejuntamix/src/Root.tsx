import {Composition} from 'remotion';
import {TechnicalTest} from './compositions/TechnicalTest';
import settings from './config/export.json';

// Presets técnicos: formato e duração reais serão decididos após análise.
export const RemotionRoot = () => (
  <>
    <Composition id="TesteHorizontal" component={TechnicalTest}
      width={settings.formats['16:9'].width} height={settings.formats['16:9'].height}
      fps={settings.fps} durationInFrames={settings.fps * settings.testSeconds} />
    <Composition id="TesteVertical" component={TechnicalTest}
      width={settings.formats['9:16'].width} height={settings.formats['9:16'].height}
      fps={settings.fps} durationInFrames={settings.fps * settings.testSeconds} />
  </>
);
