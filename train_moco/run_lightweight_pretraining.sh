# RTX 3070 8GB 优化配置
# 针对8GB显存优化，batch_size=64确保稳定运行

CUDA_VISIBLE_DEVICES=0 python3 main_moco.py \
                        -a resnet18 \
                        --lr 0.03 --batch-size 64 --multiprocessing-distributed \
                        --world-size 1 --rank 0 --aug-plus --mlp --cos --moco-align-w 0 \
                        --moco-unif-w 0 --moco-contr-w 1 --moco-contr-tau 0.2 \
                        --dist-url tcp://localhost:10066 \
                        --save-folder-root ./lightweight_ckpt/hunting-dog \
                        --experiment-id exp \
                        --epochs 50 \
                        --schedule 30,40 \
                        --workers 4 \
                        ../data/pretraining/hunting-dog_650_0.0_filelist.txt

# 注释掉的其他配置可以用于完整训练
# CUDA_VISIBLE_DEVICES=0,1 python3 main_moco.py \
#                         -a resnet18 \
#                         --lr 0.06 --batch-size 256 --multiprocessing-distributed \
#                         --world-size 1 --rank 0 --aug-plus --mlp --cos --moco-align-w 0 \
#                         --moco-unif-w 0 --moco-contr-w 1 --moco-contr-tau 0.2 \
#                         --dist-url tcp://localhost:10067 \
#                         --save-folder-root ./new_ckpt/hunting-dog-plus \
#                         --experiment-id exp \
#                         ../data/pretraining/hunting-dog_650_0.2_filelist.txt
