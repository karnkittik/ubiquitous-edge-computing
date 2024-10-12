<template>
  <h1 class="TTPD">Welcome to People Counting Services</h1>
  <p>
    This service provides counting of people using an image processing technique
    (YOLOv8) on different computing services.
  </p>
  <div class="upload-card">
    <ImageUpload title="Original Image" ref="originalImg" />
  </div>
</template>

<script setup>
import ImageUpload from "./components/ImageUpload.vue";
import { ref, computed } from "vue";
const originalImg = ref(null);
const originalImgFile = computed(() => {
  return originalImg.value.selectedFile;
});
</script>

<style scoped></style>
