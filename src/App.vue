<template>
    <h1 class="TTPD">Welcome to People Counting Services</h1>
    <p>
        This service provides counting of people using an image processing
        technique (YOLOv8) on different computing services.
    </p>
    <div class="card-pane">
        <div class="upload-card">
            <ImageUpload title="Original Image" ref="originalImg" />
        </div>
        <div class="edge-card">
            <ImageSubmit
                :isDisabled="!originalImgFile || isEdgeDisabled"
                :originalImgFile="originalImgFile"
                @disableEdge="disableEdge"
                @enableEdge="enableEdge"
                title="Edge: yolov8n"
            />
        </div>
    </div>
</template>

<script setup>
import ImageSubmit from './components/ImageSubmit.vue'
import ImageUpload from './components/ImageUpload.vue'
import { ref, computed } from 'vue'
const originalImg = ref({ selectedFile: null })
const originalImgFile = computed(() => {
    return originalImg.value.selectedFile
})
const isEdgeDisabled = ref(false)
const disableEdge = () => {
    isEdgeDisabled.value = true
}
const enableEdge = () => {
    isEdgeDisabled.value = false
}
</script>

<style scoped>
.card-pane {
    display: flex;
    flex-direction: rows;
    background-color: red;
}
</style>
