# 把这个项目上传 GitHub

建议仓库名称：`STM32-Self-Balancing-Car`。仓库描述示例见 `docs/project-introduction.md`。

## 网页上传（适合初学者）

1. 在 GitHub 创建一个公开仓库 `STM32-Self-Balancing-Car`，可勾选不预先创建 README（本包已有 README）。
2. **先解压**下载的 `STM32-Self-Balancing-Car_GitHub-Ready.zip`。GitHub 网页不会自动把 ZIP 解压成整个仓库目录。
3. 进入解压后的 `STM32-Self-Balancing-Car` 文件夹，选择里面的文件和文件夹（`Core`、`Drivers`、`examples`、`docs`、`README.md`、`CMakeLists.txt`、`BalancingCar.ioc` 等），使用 GitHub 网页中的 `Add file → Upload files` 上传；如果网页不支持直接选文件夹，可以使用 Git 命令行。
4. 上传完成后检查首页 README 是否正常渲染，目录层级是否完整。
5. 上传自己拍的实物照片/演示视频，随后修改 README 中的图片链接。

GitHub 网页上传单个文件有大小限制；命令行通常更适合完整工程。

## Git 命令行（推荐保留文件夹结构）

仓库创建后，在**解压的项目根目录**运行：

```bash
git init
git add .
git commit -m "docs: publish STM32 balancing car project"
git branch -M main
git remote add origin https://github.com/你的用户名/STM32-Self-Balancing-Car.git
git push -u origin main
```

`你的用户名` 替换成你的 GitHub 账号，首次推送需要按 GitHub 要求完成授权。**不要把 `build`、密钥文件、其他人的私有资料提交进去。**

## 发布前检查

- [ ] 确认代码的真实来源和分享许可（见 `THIRD_PARTY_NOTICES.md`）
- [ ] 不要把原固件说成 PID + FreeRTOS（实际为 LQR + 自定义调度）
- [ ] README 中的展示照片与视频确实来自你的项目
- [ ] 项目具体完成情况与简历描述一致
- [ ] 移除密码、Token、私有密钥及不宜公开的个人信息
