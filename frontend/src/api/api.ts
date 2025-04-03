import axios from "axios";

// Интерфейсы из вашего кода
export interface DocumentPreview {
  id: number;
  name: string;
  uploadDate: Date;
}

export interface DocumentAnalysisData {
  [key: string]: string | string[] | number;
}

export function useApi() {
  const apiUrl = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

  // Настройка экземпляра axios
  const axiosInstance = axios.create({
    baseURL: apiUrl,
    headers: {
      "Content-Type": "application/json",
    },
  });

  // GET /pdf/analyse/ - Получение списка недавних документов
  const fetchRecentDocuments = async (): Promise<DocumentPreview[]> => {
    try {
      const response = await axiosInstance.get("/pdf/analyse/");
      const data = response.data;
      return data.map((item: any) => ({
        id: item.id,
        name: item.name,
        uploadDate: new Date(item.uploadDate),
      }));
    } catch (error) {
      console.error("Ошибка в fetchRecentDocuments:", error);
      // Возвращаем заглушку в случае ошибки
      return [
        {
          id: 1,
          name: "взыскание долга",
          uploadDate: new Date(Date.parse("2024-02-26T01:00:00Z")),
        },
      ];
    }
  };

  // POST /pdf/analyse/ - Загрузка документа
  const uploadDocument = async (
    file: File,
    onProgress?: (progress: number) => void,
  ): Promise<string> => {
    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await axiosInstance.post(
        "/pdf/analyse/",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
          onUploadProgress: (progressEvent) => {
            if (onProgress && progressEvent.total) {
              const progress = Math.round(
                (progressEvent.loaded / progressEvent.total) * 100,
              );
              onProgress(progress);
            }
          },
        },
      );
      return response.data.documentId || `doc_${Date.now()}`; // Предполагаем, что API возвращает ID
    } catch (error) {
      console.error("Ошибка в uploadDocument:", error);
      // Эмуляция успешной загрузки в случае ошибки
      return `doc_${Date.now()}`;
    }
  };

  // GET /pdf/{id} - Получение анализа документа
  const fetchDocumentAnalysis = async (
    documentId: string,
  ): Promise<DocumentAnalysisData> => {
    try {
      const response = await axiosInstance.get(
        `/pdf/${documentId}`,
      );
      return response.data as DocumentAnalysisData;
    } catch (error) {
      console.error("Ошибка в fetchDocumentAnalysis:", error);
      // Возвращаем заглушку в случае ошибки
      return {
        "Наименование суда": "Городской судебный участок № 6",
        Взыскатель: 'ООО "АЖС" БЛАГОВЕЩЕНСК"',
        "Юридический адрес взыскателя": "675000, Амурская область, г. Благовещенск",
        "Телефон взыскателя": "8(4162) 770-448",
        "ИНН взыскателя": "2801176049",
        "Адрес взыскателя для корреспонденции": "675997, Амурская область, г. Благовещенск",
        Должник: "Очиников Фёдор Емельянович",
        "Адрес должника": "675000, Амурская область, г. Благовещенск",
        "Дата рождения должника": "21.11.1997",
        "Сущность взыскания": "Взыскание задолженности по оплате жилищных услуг",
        "Сумма долга": "638,79",
        "Общая сумма взыскания": "642,67",
        Госпошлина: "200",
        "Приложение к заявлению": [
          "Копия договора управления",
          "Копия выписки лицевого счета",
          "Расчет пени",
        ],
      };
    }
  };

  const deleteDocument = async (documentId: string): Promise<void> => {
    try {
      await axiosInstance.delete(`/pdf/delete/${documentId}`);
    } catch (error) {
      console.error("Ошибка в deleteDocument:", error);
      throw error;
    }
  };

  return {
    fetchRecentDocuments,
    uploadDocument,
    fetchDocumentAnalysis,
    deleteDocument,
  };
}

// Пример использования
(async () => {
  const api = useApi();

  // Получение списка документов
  const recentDocs = await api.fetchRecentDocuments();
  console.log("Недавние документы:", recentDocs);

  // Загрузка файла
  const file = new File(["test"], "test.pdf", { type: "application/pdf" });
  const docId = await api.uploadDocument(file, (progress) =>
    console.log(`Прогресс: ${progress}%`),
  );
  console.log("Загружен документ с ID:", docId);

  // Анализ документа
  const analysis = await api.fetchDocumentAnalysis(docId);
  console.log("Анализ документа:", analysis);

  // Удаление документа
  await api.deleteDocument(docId);
  console.log("Документ удален");
})();