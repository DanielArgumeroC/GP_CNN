import { useEffect, useState } from "react";
import { Container, ProgressBar } from "react-bootstrap";

const FileUpload = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [selectedFileDom, setSelectedFileDom] = useState(null);
  let [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  useEffect(() => {
    let interval;
    if (uploading) {
      interval = setInterval(() => {
        setProgress((prev) => prev + 1);
      }, 2000);
    }

    return () => {
      clearInterval(interval);
    };
  }, [uploading]);

  useEffect(() => {
    if (progress >= 100) {
      clearInterval(uploading);
      setUploading(false);
    }
  }, [progress]);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);
    const fileDom = URL.createObjectURL(file);
    setSelectedFileDom(fileDom);
  };

  const handleFormSubmit = async (event) => {
    event.preventDefault();

    if (!selectedFile) {
      alert("Por favor selecciona un archivo");
      return;
    }

    const formData = new FormData();
    formData.append("image", selectedFile);

    try {
      const response = await fetch("http://localhost:9000/upload", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        alert("Archivo subido correctamente");
        setProgress(0);
        setUploading(true);
      } else {
        alert("Error al subir el archivo");
      }
    } catch (error) {
      alert("Error al subir el archivo");
    }
  };

  return (
    <Container fluid style={{ textAlign: "center" }}>
      <h3>
        <b>Diagnostíquese Aquí</b>
      </h3>
      <form onSubmit={handleFormSubmit}>
        {selectedFile ? (
          <img
            src={selectedFileDom}
            className="UploadImg"
            style={{
              width: "1280px",
              height: "720px",
            }}
          />
        ) : (
          <div className="upload-container">
            <div
              className="uploadbox-wrapper d-flex flex-column align-items-center font-size-125 py-3"
              onDragOver={(e) => e.preventDefault()}
            >
              <i className="fa fa-cloud-upload-alt fa-5x vue-uploadbox-icon"></i>
              <span className="px-1 text-center vue-uploadbox-drop-text">
                Arrastra y suelta los archivos aquí
              </span>
            </div>
            <label
              htmlFor="fileInput"
              className="btn btn-light font-size-125 font-weight-bold text-nowrap vue-uploadbox-file-button position-static"
            >
              Seleccionar archivo
            </label>
            <input
              type="file"
              id="fileInput"
              style={{ display: "none" }}
              onChange={handleFileChange}
            />
          </div>
        )}
        {uploading && (
          <ProgressBar
            striped
            variant="info"
            animated
            now={progress}
            label={`${progress}%`}
            style={{
              marginTop: 20,
              width: "51%",
              height: "2rem",
              marginLeft: "24.5%",
            }}
          />
        )}
        {selectedFile && (
          <button
            type="submit"
            className="btn btn-dark"
            style={{
              marginTop: 20,
              width: "75%",
              opacity: 0.5,
              color: "white",
            }}
            disabled={uploading}
          >
            Enviar
          </button>
        )}
      </form>
    </Container>
  );
};

export default FileUpload;
