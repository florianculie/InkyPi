from plugins.base_plugin.base_plugin import BasePlugin 
from datetime import datetime
from utils.image_utils import get_image
from PIL import Image
import logging


logger = logging.getLogger(__name__)

#                                          YYYY/MM/DD/fr/newspapername
KIOSKO_IMAGE_URL = "https://img.kiosko.net/{}/{}/{}/fr/{}.750.jpg"
class FrenchNewspaper(BasePlugin):
    def generate_image(self, srttings, device_config):
        newspaper_slug = "l_equip"

        today = datetime.today()

        image_url = KIOSKO_IMAGE_URL.format(today.year, today.month, today.day, newspaper_slug)
        image = get_image(image_url)
        if image:
            logging.info(f"Found {newspaper_slug} from covert for {today.strftimer('%Y-%m-%d')}")
            # expand height if newspaper is wider than resolution
            img_width, img_height = image.size
            desired_width, desired_height = device_config.get_resolution()

            img_ratio = img_width / img_height
            desired_ratio = desired_width / desired_height

            if img_ratio < desired_ratio:
                new_height = int((img_width*desired_width) / desired_height)
                new_image = Image.new("RGB", (img_width, new_height), (255, 255, 255))
                new_image.paste(image, (0,0))
                image = new_image
        else:
            raise RuntimeError("Newspaper front cover not found.")
        return image
        



