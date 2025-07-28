document.getElementById('uploadForm').addEventListener('submit', async (e) => {
  e.preventDefault();

  const image = document.getElementById('imageInput').files[0];
  if (!image) return alert("يرجى اختيار صورة أولاً.");

  const formData = new FormData();
  formData.append('image', image);

  const response = await fetch('/process-image', {
    method: 'POST',
    body: formData
  });

  if (!response.ok) {
    alert("حدث خطأ أثناء معالجة الصورة.");
    return;
  }

  const data = await response.json();

 
  document.getElementById('result').textContent = `عدد الأعطال المكتشفة: ${data.count}`;

 
  const sev = data.severity || { high: 0, medium: 0, low: 0 };
  const severityInfo = `
    <span class="red">خطورة عالية: ${sev.high}</span> | 
    <span class="orange">متوسطة: ${sev.medium}</span> | 
    <span class="yellow">منخفضة: ${sev.low}</span>
  `;
  document.getElementById('severityInfo').innerHTML = severityInfo;

 
  const outputImage = document.getElementById('outputImage');
  outputImage.src = data.image + '?t=' + new Date().getTime(); 
  outputImage.style.display = 'block';
});
