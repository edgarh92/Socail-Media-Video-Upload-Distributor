
from dataclasses import dataclass
import datetime
import argparse
from sum_media_duration import format_duration_to_seconds, get_total_duration
from _utils import build_file_list #  TODO: set this backt to src for pytest
from VendorDB import VendorDatabase #  TODO: set this backt to src for pytest
from config import PLATFORM_TARGET_RATIOS


@dataclass(frozen=True)
class JobBatch():
    duration: datetime.timedelta
    assignment: str
    files: list


class UploadBatch():

    def __init__(self, JobBatch, VendorDB: VendorDatabase) -> None:
        self.MediaBatch = JobBatch
        self.transaction_db = VendorDB
    def check_ratio_threshhold(self, ratio:float):
        if platform_ratio < PLATFORM_TARGET_RATIOS['YOUTUBE'] : #This needs work.
            #This will add contiously. 
            #If the ratio is greater than 10 it will add to the total
            print("Commit to platformDuration")
            print("Commit to updateDatabase")
            print("Commit to orderCaptions")
            return True
        else:
            print("Commit to platformDuration")
            print("Commit to updateDatabase")
        return False

    def is_valid_order(self) -> bool:

        """ Calculate Latest platform Duration,
            estimated final duration, and platform to platform duration
            Calculate Latest Database Duration
            platform Ratio

        Returns:
            bool: Trigger upload order through platform if ratio is below 
            required threshhold
        """    
        #Calculate Ratio and Updates Database

        #Date Time Object as Seconds
        total_db_duration = datetime.timedelta().total_seconds()
        batch_duration = self.MediaBatch.duration
        platform_duration = self.transaction_db.get_vendor(
            self.MediaBatch.assingment)['duration']

        for captioned_duration in self.transaction_db.get_all_durations():
            total_db_duration += captioned_duration

        try:            
            platform_duration_from_db = platform_duration
            print("Stored platform Duration:", platform_duration_from_db)
        except:
            print('platform Does not exists')
        
        est_platform_duration = (
            batch_duration + platform_duration_from_db)

        total_db_duration = (est_platform_duration + total_db_duration)
        platform_ratio = (est_platform_duration/total_db_duration) #  Calculate ratio
        print(f'Values: \
            {platform_ratio}, {total_db_duration}, {est_platform_duration}')
            #If the addition of these durations is greater than 10% it won't order captions
        return self.check_ratio_threshhold(platform_ratio)
        

    def platform_transaction(self, is_valid_order: bool) -> None:
        '''Excute Captions Transaction'''
        pass


    def determine_platform_ratio(self) -> bool:
        """Run calculation for distribution of content and return 

        Returns:
            is_valid_transaction: Boolean to determine if transaction should occur. 
        """        

        self.MediaBatch.duration = format_duration_to_seconds(
                get_total_duration(video_file_list=self.MediaBatch.files))

        is_valid_transaction = self.is_valid_order()
        return is_valid_transaction


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Upload a video to social mediia based on total duration of existing social media uploads")
    parser.add_argument("-f", "--files", nargs="*", help="Indivudal files or directories to process")

    args = parser.parse_args()
    batch = JobBatch(
        duration=None,
        assignment='Youtube',
        files=build_file_list(args.files))
    if not batch.files:
        print('No accepted files found. Drag files or folders or both.')
    else:
        batch_transaction = UploadBatch(batch, VendorDatabase())
        transaction_status = batch_transaction.determine_platform_ratio()
        if transaction_status:
            print("Ordered Captions")
            batch_transaction.platform_transaction(transaction_status)

        else:
            print("no captions")