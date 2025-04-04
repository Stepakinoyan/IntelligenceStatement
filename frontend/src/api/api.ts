import axios from "axios";

export interface DocumentPreview {
  id: number;
  create_at: Date;
}

export interface DocumentAnalysisData {
  [key: string]: string | string[] | number;
}

export function useApi() {
  const apiUrl = import.meta.env.VITE_API_URL;

  const fetchRecentDocuments = async (): Promise<DocumentPreview[]> => {
    try {
      const response = await axios.get(`${apiUrl}/pdf/all`);
      return response.data;
    } catch (error) {
      console.error("Error fetching document analysis:", error);
      throw error;
    }
  };

  const deleteDocumentById = async (documentId: string): Promise<void> => {
    try {
      await axios.delete(`${apiUrl}/pdf/delete/${documentId}`);
    } catch (error) {
      console.error("Ошибка при удалении документа:", error);
      throw error;
    }
  };

  const uploadDocument = async (
    file: File,
    onProgress?: (progress: number) => void,
  ): Promise<string> => {
    const formData = new FormData();
    formData.append("file", file);
    console.log(file);

    try {
      const response = await axios.post(`${apiUrl}/pdf/analyse/`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        onUploadProgress: (progressEvent) => {
          if (onProgress && progressEvent.total) {
            const progress = Math.round(
              (progressEvent.loaded * 100) / progressEvent.total,
            );
            onProgress(progress);
          }
        },
      });
      return response.data.documentId;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        console.error("Ошибка загрузки:", error.response?.data);
      }
      throw error;
    }
  };

  const fetchDocumentAnalysis = async (
    documentId: string,
  ): Promise<DocumentAnalysisData> => {
    try {
      const response = await axios.get(`${apiUrl}/pdf/${documentId}`);
      return response.data;
    } catch (error) {
      console.error("Error fetching document analysis:", error);
      throw error;
    }
  };
  const downloadFileById = async (
    documentId: number,
    type: "json" | "excel",
  ): Promise<void> => {
    try {
      const response = await axios.get(
        `${apiUrl}/pdf/download/${documentId}?type=${type}`,
        {
          responseType: "blob",
        },
      );

      const fileExtension = type === "json" ? "json" : "xlsx";
      const mimeType =
        type === "json"
          ? "application/json"
          : "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet";

      const blob = new Blob([response.data], { type: mimeType });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", `document_${documentId}.${fileExtension}`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error(`Ошибка при скачивании ${type}-файла:`, error);
      throw error;
    }
  };

  return {
    fetchRecentDocuments,
    uploadDocument,
    fetchDocumentAnalysis,
    deleteDocumentById,
    downloadFileById,
  };
}
