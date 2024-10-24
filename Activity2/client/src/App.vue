<template>
    <div>
        <h1 class="TTPD">Welcome to People Counting Services</h1>
        <p class="you-left-your-typewriter-at-my-apateu">
            This service provides counting of people using an image processing
            technique (YOLOv8) on different computing services and model size.
        </p>
        <div class="card-pane">
            <div class="upload-pane">
                <ImageUpload title="Original Image" ref="originalImg" />
            </div>
            <div class="edge-card">
                <ImageSubmit
                    :isDisabled="!originalImgFile || isEdgeDisabled"
                    :api="queryService.cloudPeopleCounting"
                    :originalImgFile="originalImgFile"
                    @disableEdge="disableEdge"
                    @enableEdge="enableEdge"
                    title="Cloud"
                />
                <ImageSubmit
                    v-for="edgeService in edgeServices"
                    :key="edgeService.id"
                    :isDisabled="!originalImgFile || isEdgeDisabled"
                    :api="queryService.edgePeopleCounting"
                    :originalImgFile="originalImgFile"
                    :modelSize="edgeService.modelSize"
                    @disableEdge="disableEdge"
                    @enableEdge="enableEdge"
                    :title="`Edge:${edgeService.modelSize}`"
                />
            </div>
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
const edgeServices = ref([
    { id: 1, modelSize: 'yolov8n' },
    { id: 2, modelSize: 'yolov8s' },
    { id: 3, modelSize: 'yolov8m' },
    // Too large for Pi (RAM 2GB)
    // { id: 4, modelSize: 'yolov8l' },
    // { id: 5, modelSize: 'yolov8x' },
])
</script>

<style scoped>
.card-pane {
    display: flex;
    flex-direction: rows;
    /* background-color: red; */
}
.upload-pane {
    justify-content: flex-end;
    /* background-color: blue; */
}
.edge-card {
    display: flex;
    flex-direction: rows;
    /* background-color: yellow; */
    max-width: 100%;
    flex-wrap: wrap;
}
</style>
