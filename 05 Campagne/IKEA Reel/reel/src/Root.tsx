import React from "react";
import {Composition} from "remotion";
import {Reel} from "./Reel";
import {DUREE} from "./scenes";

export const FPS = 60;

export const Root: React.FC = () => (
  <Composition id="Reel" component={Reel} width={1920} height={1080} fps={FPS} durationInFrames={Math.round(DUREE * FPS)} />
);
