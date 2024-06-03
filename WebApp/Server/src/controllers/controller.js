import { exec } from "child_process";

// Manejador de la subida de imágenes
export const uploadImage = (req, res) => {
  if (!req.file) {
    return res
      .status(400)
      .send("Error: No se ha proporcionado ningún archivo para subir");
  }
  res.status(200).send("Imagen subida correctamente, se esta procesando...");
  console.log(req.file);

  // Ejecutar el script main.py después de subir la imagen con éxito

  const comand = "cd .. & cd .. & cd CNN - Scripts & py main.py";
  exec(comand, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error al ejecutar el script: ${error.message}`);
      return;
    }
    if (stderr) {
      console.error(`Error en la salida del script: ${stderr}`);
    }

    console.log(`Salida del script: ${stdout}`);
  });
};
