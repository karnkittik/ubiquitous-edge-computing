<script setup>
import { ref } from 'vue'
defineProps(['title'])

const selectedFile = ref(null) // Variable to store the selected file
const thumbnail = ref(null) // Variable to store the thumbnail Data URL
const base64Image = ref('')
const previewImage = (event) => {
    const file = event.target.files[0]
    if (file) {
        selectedFile.value = file // Store the selected file
        const reader = new FileReader()
        reader.onload = (e) => {
            thumbnail.value = e.target.result // Store the Data URL for thumbnail preview
            base64Image.value = reader.result.split(',')[1] // Removes the data:image part
        }
        reader.readAsDataURL(file)
    }
}
defineExpose({
    base64Image,
})
</script>
<template>
    <div class="upload-card">
        <h1 class="title">{{ title }}</h1>
        <p class="note">File size should not exceed 5 MB</p>
        <div class="card">
            <input
                type="file"
                accept="image/png, image/gif, image/jpeg"
                @change="previewImage"
                class="upload-form"
            />
            <div v-if="thumbnail" class="thumbnail-preview">
                <img :src="thumbnail" alt="Uploaded Image" class="thumbnail" />
            </div>
        </div>
    </div>
</template>

<style scoped>
.upload-card {
    width: 260px;
    min-height: 260px;
    margin: 20px;
    padding: 20px;
    text-align: center;
    /* border: 1px solid #ddd; */
    border-radius: 8px;
    /* background-color: #f9f9f9; */
    /* box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); */
}

.title {
    font-size: 24px;
    color: #333;
    margin-bottom: 10px;
}

.card {
    padding: 0;
    overflow: hidden;
}

.note {
    font: small-caption;
    color: rgb(163, 93, 196);
    margin-bottom: 5px;
    color: #6e5aa5;
    font-weight: bolder;
}

.thumbnail-preview {
    margin-top: 20px;
}

.thumbnail {
    max-width: 100%;
    max-height: 100%;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    object-fit: contain;
}
</style>
