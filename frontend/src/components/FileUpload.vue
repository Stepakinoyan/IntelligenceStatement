<template>
  <div
    class="file-upload"
    @dragover.prevent="dragOver = true"
    @dragleave="dragOver = false"
    @drop.prevent="handleDrop"
    :class="{ 'drag-over': dragOver }"
  >
    <div v-if="!isUploading" class="upload-content">
      <p>Перетащите PDF файл сюда или</p>
      <input
        type="file"
        id="file-input"
        accept=".pdf"
        @change="handleFileSelect"
        hidden
      />
      <label for="file-input" class="browse-button">Выберите файл</label>
    </div>
    <div v-else class="upload-progress">
      <p>Загрузка файла...</p>
      <progress :value="uploadProgress" max="100"></progress>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useApi } from "@/api/api";

const emit = defineEmits(["upload-success"]);

const { uploadDocument } = useApi();
const dragOver = ref(false);
const isUploading = ref(false);
const uploadProgress = ref(0);

const handleFileSelect = async (e: Event) => {
  const input = e.target as HTMLInputElement;
  if (input.files && input.files.length > 0) {
    await processFile(input.files[0]);
  }
};

const handleDrop = async (e: DragEvent) => {
  dragOver.value = false;
  if (e.dataTransfer && e.dataTransfer.files.length > 0) {
    await processFile(e.dataTransfer.files[0]);
  }
};

const processFile = async (file: File) => {
  if (file.type !== "application/pdf") {
    alert("Пожалуйста, загрузите файл в формате PDF");
    return;
  }

  try {
    isUploading.value = true;
    const documentId = await uploadDocument(file, (progress: number) => {
      uploadProgress.value = progress;
    });
    emit("upload-success", documentId);
  } catch (error) {
    console.error("Ошибка загрузки файла:", error);
    alert("Произошла ошибка при загрузке файла");
  } finally {
    isUploading.value = false;
    uploadProgress.value = 0;
  }
  emit("upload-success", 1);
};
</script>

<style scoped>
.file-upload {
  border: 2px dashed #ccc;
  border-radius: 8px;
  padding: 2rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.file-upload.drag-over {
  border-color: #42b983;
  background-color: rgba(66, 185, 131, 0.1);
}

.upload-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.browse-button {
  display: inline-block;
  padding: 0.5rem 1rem;
  background-color: #42b983;
  color: white;
  border-radius: 4px;
  cursor: pointer;
}

.upload-progress {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

progress {
  width: 100%;
  height: 8px;
}
</style>
