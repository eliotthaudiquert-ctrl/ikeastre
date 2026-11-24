import React from "react";
import {Composition} from "remotion";
import {Fika, DUREE} from "./Fika";

export const FPS = 60;

export const Root: React.FC = () => (
  <Composition id="Fika" component={Fika} width={1920} height={1080} fps={FPS} durationInFrames={Math.round(DUREE * FPS)} />
);
