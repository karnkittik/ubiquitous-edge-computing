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
                :api="queryService.edgePeopleCounting"
                :originalImgFile="originalImgFile"
                :modelSize="'yolov8n'"
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
import queryService from './service/api'
const originalImg = ref({ base64Image: '' })
const originalImgFile = computed(() => {
    return originalImg.value.base64Image
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
