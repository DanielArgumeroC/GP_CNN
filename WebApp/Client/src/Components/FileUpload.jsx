import { useState, useEffect } from "react";
import { Container, ProgressBar } from "react-bootstrap";

const FileUpload = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [selectedFileDom, setSelectedFileDom] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [diagnosisComplete, setDiagnosisComplete] = useState(false);

  useEffect(() => {
    let interval;
    if (uploading) {
      interval = setInterval(() => {
        setProgress((prev) => (prev < 100 ? prev + 1 : prev));
      }, 2000);
    } else {
      clearInterval(interval);
      if (progress >= 100) {
        const diagnosis = Math.random() < 0.5 ? "Negativo" : "Positivo";
        setDiagnosisComplete(true);
        setTimeout(() => {
          alert(`Su diagnóstico es: ${diagnosis}`);
          setSelectedFile(null);
          setSelectedFileDom(null);
          setProgress(0);
        }, 5000);
      }
    }

    return () => {
      clearInterval(interval);
    };
  }, [uploading]);

  useEffect(() => {
    if (progress >= 100) {
      setUploading(false);
    }
  }, [progress]);

  useEffect(() => {
    let timer;
    if (uploading) {
      timer = setTimeout(() => {
        setDiagnosisComplete(true);
        setUploading(false);
        setProgress(100);
      }, 360000); // 6 minutes in milliseconds
    }

    return () => clearTimeout(timer);
  }, [uploading]);

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
        console.log(response.json.data);
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
        <b>
          {diagnosisComplete
            ? "Su diagnóstico es:"
            : uploading
            ? "Diagnosticando..."
            : "Diagnostíquese Aquí"}
        </b>
      </h3>
      <form onSubmit={handleFormSubmit}>
        {uploading ? (
          <video
            src="../../public/video/loading.mp4"
            autoPlay
            loop
            muted
            style={{
              width: "35%",
              height: "10%",
              alignItems: "center",
              filter: "drop-shadow(0 0 0.75rem #fff)",
              position: "relative",
            }}
            className="loading-video"
          />
        ) : diagnosisComplete ? (
          <img
            src={
              diagnosisComplete === "Positivo"
                ? "../../public/Positive.png"
                : "../../public/Negative.png"
            }
            className="DiagnosisImg"
            style={{ width: "500px", height: "500px" }}
          />
        ) : selectedFile ? (
          <img
            src={selectedFileDom}
            className="UploadImg"
            style={{ width: "500px", height: "500px" }}
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
        {selectedFile && !uploading && !diagnosisComplete && (
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
        {diagnosisComplete && (
          <div className="response">
            <p>
              Gracias por esperar. Tu diagnóstico ha sido completado. Por favor
              revisa la imagen de arriba para ver los resultados.
            </p>
          </div>
        )}
      </form>
    </Container>
  );
};

export default FileUpload;
