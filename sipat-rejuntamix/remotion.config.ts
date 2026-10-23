import {Config} from '@remotion/cli/config';
import settings from './src/config/export.json';

Config.setRspack(true);
Config.setVideoImageFormat('jpeg');
Config.setCodec('h264');
Config.setPixelFormat('yuv420p');
Config.setColorSpace('bt709');
Config.setCrf(settings.crf);
Config.setConcurrency(settings.threads);
Config.setBrowserExecutable(process.env.REMOTION_BROWSER_EXECUTABLE ?? '/usr/bin/chromium');
Config.setOverwriteOutput(false);
