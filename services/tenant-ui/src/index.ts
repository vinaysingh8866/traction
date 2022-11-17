import config from "config";
import cors from "cors";
import express from "express";
import path from "path";

import { router } from "./routes/router";
import { tractionProxy } from "./routes/tractionRouter";
import { acapyProxy } from "./routes/acapyRouter";
import { handleAcapy } from "./middelware/acapy";

const PORT: number = parseInt(config.get("server.port") as string, 10);
const APIROOT: string = config.get("server.apiPath");
const PROXYROOT: string = config.get("server.proxyPath");
const PROXYACAPYROOT: string = config.get("server.proxyAcapyPath");
const STATIC_FILES_PATH: string = config.get("server.staticFiles");

import history from "connect-history-api-fallback";




const app = express();
app.use(history());
app.use(cors());
app.use(express.json());
// app.use(bodyParser.json());

// Host the static frontend assets
app.use("/favicon.ico", (_, res) => {
  res.redirect("/favicon.ico");
});
app.use("/", express.static(path.join(__dirname, STATIC_FILES_PATH)));

// Frontend configuration endpoint, return config section at /config so UI can get it
app.use("/config", (_, res, next) => {
  try {
    // if we have passwords or sensitive information, strip it out!!!
    res.status(200).json(config);
  } catch (err) {
    next(err);
  }
});

// This service's api endpoints
app.use(APIROOT, router);

// Proxy any api/traction/acapy calls over to acapy
// This is just to support developing the FE against both paths for now
// See comments in acapy.ts middleware
app.use(`${PROXYACAPYROOT}/`, handleAcapy, acapyProxy);

// Proxy any api/traction calls over to Traction
app.use(`${PROXYROOT}`, tractionProxy);

app.listen(PORT, () => {
  console.log(`Listening on port ${PORT}`);
});
