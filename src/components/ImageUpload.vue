<script setup>
import { ref, defineExpose } from 'vue'
defineProps(['title'])

const selectedFile = ref(null) // Variable to store the selected file
const thumbnail = ref(null) // Variable to store the thumbnail Data URL

const previewImage = (event) => {
    const file = event.target.files[0]
    if (file) {
        selectedFile.value = file // Store the selected file
        const reader = new FileReader()
        reader.onload = (e) => {
            thumbnail.value = e.target.result // Store the Data URL for thumbnail preview
        }
        reader.readAsDataURL(file)
    }
}
defineExpose({
    selectedFile,
})
</script>
<template>
    <div class="upload-card">
        <h1 class="title">{{ title }}</h1>
        <div class="card">
            <input type="file" accept="image/*" @change="previewImage" />
            <div v-if="thumbnail" class="thumbnail-preview">
                <img :src="thumbnail" alt="Uploaded Image" class="thumbnail" />
            </div>
        </div>
    </div>
</template>

<style scoped>
.upload-card {
    width: 300px;
    height: 300px;
    margin: 20px;
    padding: 20px;
    text-align: center;
    border: 1px solid #ddd;
    border-radius: 8px;
    background-color: #f9f9f9;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.title {
    font-size: 24px;
    color: #333;
}

.card {
    padding: 20px;
}

.thumbnail-preview {
    margin-top: 20px;
}

.thumbnail {
    max-width: 100%;
    height: auto;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}
</style>
