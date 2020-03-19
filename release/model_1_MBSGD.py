# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/3/20 0:49
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmail.com
# ------------------------------------
from R0_Plus.core.dataloader import DataLoader
from R0_Plus.core.models import LogisticRegression
from R0_Plus.core.common import *

import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(process)d %(name)s: %(message)s")


@calc_time
def train(model, train_data_loader):
	# 模型训练
	logging.info("Start Training!")
	max_iterations = MAX_ITERATIONS
	for epoch in range(EPOCHS):
		for i, (X, Y) in enumerate(train_data_loader, 0):
			model.fit(X, Y)

			if LOG_LEVEL <= logging.DEBUG and (i + 1) % LOG_INTERVAL == 0:
				eval_result = model.evaluate(model.predict(train_data_loader.X_to_valid), train_data_loader.Y_to_valid)
				logging.debug("epoch: [{}/{}], iter: [{}/{}], err: [{}/{}], acc: {:.2f}%, loss: {:.6f}".format(
					(epoch + 1), EPOCHS, i + 1, len(train_data_loader), *eval_result.values()))
			max_iterations -= 1
			if max_iterations < 0:
				logging.info("Stopped training for reaching max iterations of {}".format(MAX_ITERATIONS))
				return
	else:
		logging.info("Stopped training for reaching max epochs of {}".format(EPOCHS))
		return


@calc_time
def main():
	# 加载训练集
	train_data_loader = DataLoader(
		shuffle=SHUFFLE, use_mp=ENABLE_MULTI_PROCESSES,
		batch_size=BATCH_SIZE, split_ratio=SPLIT_RATIO)
	train_data_loader.load_XY(train_data_path)

	# 模型初始化
	lr = LogisticRegression(lr=LR)
	lr.init_weight(train_data_loader.N_features)

	# 模型训练
	train(lr, train_data_loader)

	# 加载预测集
	test_data_loader = DataLoader(use_mp=ENABLE_MULTI_PROCESSES)
	test_data_loader.load_X(test_data_path)
	test_data_loader.load_Y(test_answer_path)

	# 模型预测
	Y_pred = lr.predict(test_data_loader.X)
	lr.save_prediction(Y_pred, path=test_predict_path)

	# 模型评估与持久化
	if LOG_LEVEL <= logging.INFO:
		test_result = lr.evaluate(Y_pred, test_data_loader.Y)
		logging.info("[TEST RESULT] err: [{}/{}], acc: {:.2f}%".format(*test_result.values()))
		lr.dump_weight(WEIGHTS_PATH)


if __name__ == '__main__':
	ENABLE_MULTI_PROCESSES = True
	SHUFFLE = True  # 是否打乱训练数据顺序
	SPLIT_RATIO = 0.9  # 切割训练集与验证集比率
	LOG_INTERVAL = 10
	WEIGHTS_PATH = "w.pkl"
	MAX_ITERATIONS = 100000  # 预期迭代次数计算公式： N_to_train / BS * Epochs

	"""
	经测试比较好的结果是
	"""
	LR = 0.01
	BATCH_SIZE = 10
	EPOCHS = 10

	LOG_LEVEL = logging.WARNING
	main()
