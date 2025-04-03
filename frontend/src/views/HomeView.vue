<template>
  <div class="home">
    <div class="container">
      <FileUpload
        class="upload-section"
        @upload-success="handleUploadSuccess"
      />
      <DocumentList class="document-list" :documents="recentDocuments" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import FileUpload from "@/components/FileUpload.vue";
import DocumentList from "@/components/DocumentList.vue";
import { useApi, type DocumentPreview } from "@/api/api";

const { fetchRecentDocuments } = useApi();
const router = useRouter();

const recentDocuments = ref<DocumentPreview[]>([]);

onMounted(async () => {
  recentDocuments.value = await fetchRecentDocuments();
});

const handleUploadSuccess = (documentId: string) => {
  router.push({ name: "analysis", params: { id: documentId } });
};
</script>

<style scoped>
.home {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.container {
  @media (min-width: 480px) {
    display: flex;
    flex: 1;
    gap: 64px;
  }
}

.upload-section {
  flex: 1;
}

.document-list {
  @media (max-width: 480px) {
    margin-top: 32px;
  }
  flex: 1;
  max-width: 400px;
}
</style>
