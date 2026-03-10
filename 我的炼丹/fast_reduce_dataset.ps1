# PowerShell快速数据集缩减脚本
# 直接使用PowerShell命令进行高效的文件复制

param(
    [string]$SourceDir = "E:\imagenet\corrupt-image-A",
    [string]$TargetDir = "E:\imagenet\reduced-image-A",
    [double]$Ratio = 0.3,
    [int]$MinImages = 100
)

Write-Host "🚀 开始快速数据集缩减..." -ForegroundColor Green
Write-Host "📊 缩减比例: $Ratio (保留$([int]($Ratio*100))%)" -ForegroundColor Yellow
Write-Host "📁 每类最少保留: $MinImages 张图像" -ForegroundColor Yellow

# 获取所有类别文件夹
$classDirs = Get-ChildItem -Path $SourceDir -Directory
$totalClasses = $classDirs.Count
Write-Host "📂 发现类别数量: $totalClasses" -ForegroundColor Cyan

$processedCount = 0
$totalImages = 0

foreach ($classDir in $classDirs) {
    $className = $classDir.Name
    $targetClassDir = Join-Path $TargetDir $className

    # 检查目标目录是否已存在且有足够文件
    if ((Test-Path $targetClassDir) -and
        ((Get-ChildItem -Path $targetClassDir -Filter "*.JPEG" -File).Count -ge $MinImages)) {
        $existingCount = (Get-ChildItem -Path $targetClassDir -Filter "*.JPEG" -File).Count
        Write-Host "⏭️  $className`: 已存在 $existingCount 张图像 (跳过)" -ForegroundColor Gray
        $processedCount++
        $totalImages += $existingCount
        continue
    }

    # 获取该类别的所有图像文件
    $imageFiles = Get-ChildItem -Path $classDir.FullName -Filter "*.JPEG" -File

    if ($imageFiles.Count -eq 0) {
        Write-Host "⚠️  $className`: 无图像文件 (跳过)" -ForegroundColor Yellow
        $processedCount++
        continue
    }

    # 计算要保留的图像数量
    $keepCount = [math]::Max([int]($imageFiles.Count * $Ratio), $MinImages)
    $keepCount = [math]::Min($keepCount, $imageFiles.Count)

    # 随机选择要保留的图像
    $selectedImages = $imageFiles | Get-Random -Count $keepCount

    # 创建目标类别目录
    if (!(Test-Path $targetClassDir)) {
        New-Item -ItemType Directory -Path $targetClassDir -Force | Out-Null
    }

    # 复制选中的图像
    foreach ($image in $selectedImages) {
        Copy-Item -Path $image.FullName -Destination $targetClassDir -Force
    }

    Write-Host "✅ $className`: $($imageFiles.Count) -> $keepCount 张图像" -ForegroundColor Green
    $processedCount++
    $totalImages += $keepCount

    # 显示进度
    $progress = [int](($processedCount / $totalClasses) * 100)
    Write-Progress -Activity "处理类别" -Status "$processedCount/$totalClasses ($progress%)" -PercentComplete $progress
}

Write-Host "`n🎉 处理完成!" -ForegroundColor Green
Write-Host "📊 总类别数: $processedCount" -ForegroundColor Cyan
Write-Host "🖼️  保留图像总数: $totalImages" -ForegroundColor Cyan
Write-Host "💾 目标目录: $TargetDir" -ForegroundColor Cyan

# 计算文件大小
try {
    $originalSize = (Get-ChildItem -Path $SourceDir -Recurse -File | Measure-Object -Property Length -Sum).Sum
    $reducedSize = (Get-ChildItem -Path $TargetDir -Recurse -File | Measure-Object -Property Length -Sum).Sum
    $savedSize = $originalSize - $reducedSize

    Write-Host ("`n📈 原始大小: {0:N2} GB" -f ($originalSize / 1GB)) -ForegroundColor White
    Write-Host ("📉 缩减后大小: {0:N2} GB" -f ($reducedSize / 1GB)) -ForegroundColor White
    Write-Host ("💰 节省空间: {0:N2} GB ({1:P1})" -f ($savedSize / 1GB), ($savedSize / $originalSize)) -ForegroundColor Green
} catch {
    Write-Host "⚠️  无法计算磁盘空间节省" -ForegroundColor Yellow
}

Write-Host "`n🚀 下一步操作:" -ForegroundColor Green
Write-Host "1. 运行 python run_reduced_experiment.py 开始实验" -ForegroundColor White
Write-Host "2. 或手动执行各个步骤进行调试" -ForegroundColor White




