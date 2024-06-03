import express from "express";
import multer from "multer";
import { uploadImage } from "../controllers/controller.js";
const router = express.Router();

import fs from "fs";
import path from "path";
import { dirname } from "path";
import { fileURLToPath } from "url";

// Ruta de la carpeta de subidas
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const uploadDir = path.join(__dirname, "../../uploads");
const diskstorage = multer.diskStorage({
  destination: uploadDir,
  filename: (req, file, cb) =>
    cb(null, Date.now() + "image" + file.originalname),
});

const upload = multer({
  storage: diskstorage,
}).single("image");

router.get("/upload", (req, res) => {
  res.send(`
      <h1>Imagen en tratamiento</h1>
    `);
});

router.get("/", (req, res) => {
  res.send(`
      <h1>Bienvenido a mi aplicación</h1>
      <p>Ir a la página de subida de imágenes: <a href="/upload">Subir imagen</a></p>
    `);
});

router.post("/upload", upload, uploadImage);

export default router;
